import type { NextPage } from 'next'
import { useState, useRef } from 'react'
import { IoClose } from 'react-icons/io5'
import loadData, { datt_type } from './LoadData'
import { dattAMshState, nirdhAraNState } from 'state'
import { useAtom } from 'jotai'

const Nirdharanam: NextPage = () => {
    const [nirdharan, set_nirdharan] = useAtom(nirdhAraNState)
    const [datt, shravya_datt] = useAtom(dattAMshState)
    const [loc, setLoc] = useState("");
    const [msg, setMsg] = useState(false);
    const inptRef = useRef<HTMLInputElement>(null!)
    const store = async () => {
        if (loc === '')
            return
        let v: datt_type = await loadData(loc)
        if (JSON.stringify(v) !== '{}') {
            window.localStorage.setItem("sthAnam", loc)
            shravya_datt(v)
            setMsg(true)
            setLoc('')
        }
        else {
            let el = inptRef.current.style
            el.color = "red";
            el.backgroundColor = "white";
            setTimeout(() => {
                el.color = "";
                el.backgroundColor = "";
            }, 600)
        }
    }
    return <>
        {nirdharan && <div className='fixed bottom-7 left-7'>
            <div className="">
                <input type="text" ref={inptRef} value={loc} onChange={(e) => setLoc(e.target.value)} className='w-52 p-1 ml-0 text-white bg-black font-medium m-1 border-2 border-white rounded-lg' />
                <button onDoubleClick={store} className='text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-blue-400 active:border-green-500'>ok</button>
                <button onClick={() => setMsg(true)} className='text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-red-400 active:border-green-500'>s</button>
                <IoClose onClick={() => set_nirdharan(false)} className='w-12 h-12 cursor-pointer -ml-1 inline-block fill-red-500' />
            </div>
            {(() => {
                if (!msg)
                    return <></>
                else
                    return <div className='text-white text-sm overflow-scroll max-w-xs max-h-32'>
                        <div>{window.localStorage.getItem("sthAnam")}</div>
                        <br /><div>{JSON.stringify(datt)}</div>
                    </div>
            })()}
        </div>
        }
    </>
}
export default Nirdharanam