from stftpitchshift import StftPitchShift
import scipy.io.wavfile as wavf
import numpy as np
import random
import os
import time
import sys
from plortress import definitions as d

def GIM(speech, bpm, beats):
    err = ''; fname = ''
    rate = 48000
    form = 0.003

    threshold = 2000
    gap = 5; skip = 3
    fin = np.array([])
    rep = 8

    fslice = 100
    pitchshifter = StftPitchShift(1024, 256, 48000)
    inst = np.array(wavf.read(f'{d.GEN_PATH}/audio/insts/1.wav')[1]).T[0]

    #초기멜로디 생성, 랜덤법
    b = random.randint(2,4) #반복 최소 단위
    ref = random.randint(28,38) #기준음
    refs = [ref, ref+random.randint(3,4), ref+7] #기준음들
    melody = random.choices(refs,k=b) #랜덤 멜로디
    remover = np.array([i**2 for i in range(b)]).astype(np.float32); remover /= sum(remover) #음 제거 확률
    print(remover)
    remloc = np.random.choice(b,random.randint(0,b-1),p=remover,replace=False)
    for i in remloc: melody[i]=0
    print(melody)

    melody = melody*(rep//b)+melody[:rep%b] #1단위 내에서의 반복

    #Chord가 속한 조 판별
    refs+=[refs[refs[1]-refs[0]<refs[2]-refs[1]]+2,
           refs[refs[1]-refs[0]>refs[2]-refs[1]]+random.randint(1,2)]
    refs+=[ref+8+(abs(refs[-2]-refs[-1]) in [3,refs[1]-refs[0]])]
    refs+=[ref+10+(refs[-1]-refs[-2]+random.random()<4.5)]
    refs.sort()
    print(refs)
    omni = np.concatenate([np.array(refs)+12*(i-1) for i in range(3)])
    print(omni)

    #새로운 Chord 결정
    if beats.isdigit():
        if 0<int(beats)<=16:
            for j in range(int(beats)-1):
                print(ref)
                print(np.where(omni==ref))
                ref = omni[np.where(omni==ref)[0]+(-1)**random.randrange(2)*random.randrange(4)]
                print(f'ref: {ref}')
                ref += ref+7 not in omni
                newm = random.choices([ref, (ref+3)+(ref+3 not in omni), ref+7],k=b)
                for i in remloc: newm[i]=0
                melody += newm*(rep//b)+newm[:rep%b]
        else: err = '박자수 값이 너무 크거나 0이에요.'
    else: err = '박자수 값이 잘못된 형태라서 연산할 수 없어요.'

    if len(melody)==rep*int(beats):
        if bpm.isdigit():
            if 60<=int(bpm)<=240:
                fpb = 60*rate//int(bpm)
                for i in melody:
                    if i==0: fin = np.append(fin,[0]*(fpb//2)); continue
                    print(inst[fslice:fslice+(fpb//2)])
                    temp = pitchshifter.shiftpitch(inst[fslice:fslice+(fpb//2)], 2**((i-37)/12), form)
                    print(f'fin 길이: {len(fin)}')
                    fin = np.append(fin,temp)
                fin = np.int16(fin / np.max(np.abs(fin)) * 32767)
            else: err = 'BPM 값은 60 이상 240 이하만 가능해요.'
        else: err = 'BPM 값이 잘못된 형태라서 연산할 수 없어요.'
    else: err = '연산 중 문제가 생겼어요.'

    lyr = np.array([])
    if speech in ['열병식']:
        path = f'{d.GEN_PATH}/audio/speech_div/{speech}'
        if os.path.exists(path):
            if len(os.listdir(path)) > 0:
                ended = True; a = 0
                for i in range(len(melody)):
                    if ended: a = 0; r = random.choice(os.listdir(path))
                    if not ended or str(r).endswith('.wav'):
                        if ended: r = np.array(wavf.read(f'{path}/{r}')[1]).T
                        ended = False
                        print(f'lyr 길이: {len(lyr)}')
                        if len(r)-(fpb//2)*a<fpb//2: lyr = np.concatenate((lyr,r[fpb//2*a:],[0]*(fpb//2*(a+1)-len(r)))); ended=True
                        else: lyr = np.append(lyr, r[fpb//2*a:fpb//2*(a+1)])
                    else: err = '적절한 파일을 발견하는 것에 실패했어요.'; break
                    a += 1
                lyr = np.int16(lyr / np.max(np.abs(lyr)) * 32767)
            else: err = '발언집에서 파일을 발견하는 것에 실패했어요.'
        else: err = f"'{speech}' 발언집에 내용이 없어요. 개발자를 호출해 주세요."
    else: err = f"'{speech}'(이)라는 이름의 발언집은 아직 등록되지 않았거나 존재하지 않아요."

    percs = np.zeros((fpb//2)*len(melody))
    path = f'{d.GEN_PATH}/audio/percs'
    if os.path.exists(path):
        if len(os.listdir(path)) > 0:
            for i in range(3):
                perc = np.array([])
                r = random.choice(os.listdir(path))
                if r.endswith('.wav'):
                    r = np.array(wavf.read(f'{path}/{r}')[1]).T[0]
                    beatgap = random.choice([1,2,3,4,8])
                    pattern = [1]+[0]*(beatgap-1)
                    pattern = pattern*(rep//beatgap)+pattern[:rep%beatgap]
                    for j in range(len(melody)):
                        if pattern[j%rep]==0: perc = np.append(perc, [0]*(fpb//2)); continue
                        if len(r) < fpb//2: perc = np.concatenate((perc, r, [0]*(fpb//2-len(r))))
                        else: perc = np.append(perc, r[:fpb//2])
                        print(len(perc), len(melody))
                    perc = np.int16(perc / np.max(np.abs(perc)) * 32767)
                    percs += perc
                else: err = '적절한 파일을 발견하는 것에 실패했어요.'; break
            percs = np.int16(percs / np.max(np.abs(percs)) * 32767)
            file = lyr // 3 + fin // 7 + percs // 4
            file = np.int16(file / np.max(np.abs(file)) * 32767)
            fname = f'{d.ROOT_DIR}/generated/gim_{round(time.time())}.wav'
            wavf.write(fname, 48000, file)
        else: err = '타악기를 발견하는 것에 실패했어요.'
    else: err = f"'{speech}' 타악기 파일이 없어요. 개발자를 호출해 주세요."
    return fname, err