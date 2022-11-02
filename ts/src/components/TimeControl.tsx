import type { NextPage } from 'next'
import type { MutableRefObject } from 'react'
import { useState } from 'react'

const Main: NextPage<{ elm: MutableRefObject<HTMLVideoElement> }> = ({ elm }) => {
    const [tm_show, set_tm_show] = useState(false)
    const [Hrs, setHrs] = useState('')
    const [Min, setMin] = useState('')
    const [Sec, setSec] = useState('')
    const hide_show = () => set_tm_show(!tm_show)
    const load_current = () => {
        let dur = elm.current.currentTime;
        let sec = dur % 60;
        dur -= sec;
        dur /= 60;
        sec = Math.trunc(sec);
        let min = dur % 60;
        dur -= min;
        dur /= 60;
        let hrs = dur % 60;
        setHrs(hrs.toString())
        setMin(min.toString())
        setSec(sec.toString())
    }
    const set_current = () => {
        let t = parseInt(Sec)
        t += parseInt(Min) * 60
        t += parseInt(Hrs) * 3600
        elm.current.currentTime = t
    }
    const lower_time = () => {
        elm.current.currentTime -= 10;
        load_current()
    }
    const higher_time = () => {
        elm.current.currentTime += 10;
        load_current()
    }
    return <>
        <div className='mb-2.5 mt-4'>
            <button onClick={hide_show} className={`text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-green-300 active:border-green-500 ${!tm_show ? '' : 'hidden'}`}>Show</button>
            <button onClick={hide_show} className={`text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-red-300 active:border-red-500 ${tm_show ? '' : 'hidden'}`}>Hide</button>
        </div>
        <div className={`mb-2.5 mt-5 ${tm_show ? '' : 'hidden'}`}>
            <span onClick={lower_time} className="text-2xl text-white font-bold border-2 rounded-lg p-[3px] cursor-pointer active:text-red-300 active:border-red-400">-</span>
            <span>
                <input type="number" value={Hrs} onChange={(e) => setHrs(e.target.value)} className="w-10 border-2 border-yellow-200 text-green-300 bg-black font-medium m-2 rounded" />
                <span className='font-semibold text-2xl text-white'>:</span>
                <input type="number" value={Min} onChange={(e) => setMin(e.target.value)} className="w-10 border-2 border-yellow-200 text-green-300 bg-black font-medium m-2 rounded" />
                <span className='font-semibold text-2xl text-white'>:</span>
                <input type="number" value={Sec} onChange={(e) => setSec(e.target.value)} className="w-10 border-2 border-yellow-200 text-green-300 bg-black font-medium m-2 rounded" />
            </span>
            <span onClick={higher_time} className="text-2xl text-white font-bold border-2 rounded-lg p-[3px] cursor-pointer active:text-green-300 active:border-green-400">+</span>
            <div className='mt-3'>
                <button onClick={load_current} className='text-white p-1 border-2 border-red-400 m-1 rounded-md active:text-yellow-500 active:border-blue-500'>Load</button>
                <button onClick={set_current} className='text-white p-1 border-2 border-red-400 m-1 rounded-md active:text-yellow-500 active:border-blue-500'>Set</button>
            </div>
        </div>
    </>
}
export default Main