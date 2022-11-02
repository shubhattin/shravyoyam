import { atom } from "jotai";
import type { datt_type } from "components/LoadData";
export const blinkState = atom(false, (_get, set) => {
    set(blinkState, true)
    setTimeout(() => set(blinkState, false), 400)
})
export const nirdhAraNState = atom(false)
export const lasanState = atom(false, (_get, set, val: boolean) => {
    set(lasanState, val)
    if (val == false)
        set(lasanSanchitState, ['', ['', '', 0]])
})
export const lasanSanchitState = atom<[string, [string, string, number]]>(['', ['', '', 0]])
export const mediaShowState = atom(false, (_get, set, val: (boolean | number) = -1) => {
    if (val == -1)
        set(mediaShowState, !_get(mediaShowState))
    else
        set(mediaShowState, val)
})
export const dattAMshState = atom<datt_type>({})