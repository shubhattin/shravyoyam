import type { NextPage } from 'next'
import type { ChangeEvent } from 'react'
import Head from 'next/head'
import dynamic from 'next/dynamic'
import { useState, useRef, useEffect } from 'react'
import { blinkState, nirdhAraNState, lasanState, lasanSanchitState, mediaShowState, dattAMshState } from 'state'
import { useAtom, useAtomValue, useSetAtom } from 'jotai'
import loadData, { datt_type } from 'components/LoadData'
const Blink = dynamic(() => import('components/Blink'), { ssr: false })
const Nirdharanam = dynamic(() => import('components/Nirdharanam'), { ssr: false })
const TimeControl = dynamic(() => import('components/TimeControl'), { ssr: false })
const Home: NextPage = () => {
  // global states
  const set_nirdharan = useSetAtom(nirdhAraNState)
  const [lasan, lasitam] = useAtom(lasanState)
  const [file, set_lasan_file] = useAtom(lasanSanchitState)
  const data: datt_type = useAtomValue(dattAMshState)
  const [media_show, set_media_show] = useAtom(mediaShowState)
  const blink = useSetAtom(blinkState)
  // internal states
  const [prachalan, prachalitam] = useState(false)
  const [chalan, chalitam] = useState(false)
  const [value, setValue] = useState("")
  const [selectValue, setSelectValue] = useState("")
  // end states
  let collect: number[] = []
  const media_ref = useRef<HTMLVideoElement>(null!)
  const set_media_file = (vl: string) => {
    if (vl != "" && vl in data) {
      lasitam(true)
      set_lasan_file([vl, data[vl]])
      prachalitam(false)
      set_media_show(false)
      setSelectValue(vl)
    }
    setValue("")
    if (vl != "")
      collect = []
  }
  const todani = (n: number) => {
    collect.push(n)
    if (prachalan && n === 1 && collect.length == 1)
      set_media_file(value)
    let jn = collect.join("");
    if (chalan) {
      if (jn === "12")
        prachalitam(true)
      else if (jn == "21") {
        chalitam(false) //active state of app
        prachalitam(false) //active state of input field
        lasitam(false) // state of current playback
      }
      if (jn.length === 2) {
        collect = []
        blink()
      }
    }
    else {
      if (jn === "22112") {
        let el = body.current;
        el.style.backgroundColor = 'purple'
        setTimeout(() => {
          el.style.backgroundColor = ''
          chalitam(true)
        }, 500)
      }
      else if (jn == "22212")
        set_nirdharan(true)
      if (collect.length === 5) {
        collect = [];
        blink();
      }
    }
  }
  const key_num = useRef(0);
  const check = (e: ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value)
    if (prachalan) {
      key_num.current++;
      setTimeout(() => {
        if (key_num.current == 0)
          return;
        else if (key_num.current == 1)
          setValue('')
        key_num.current--;
      }, 3000)
    } else
      setValue('');
  }
  const body = useRef<HTMLDivElement>(null!)
  return <div ref={body} className={`body w-screen h-screen ${JSON.stringify(data) !== "{}" ? 'bg-black' : 'bg-stone-900'} select-none p-2 fixed top-0`}>
    <Head>
      <title>లస్యశ్రవ్యౌ</title>
      <link rel="icon" href="favicon.png" />
    </Head>
    <>
      <div className={prachalan ? '' : 'hidden'}>
        <form onSubmit={(e) => { e.preventDefault(); set_media_file(value) }}>
          <input onChange={check} value={value} type="text" className='w-52 ml-0 text-teal-500 bg-black block font-semibold m-1 text-xl border-2 border-gray-900 rounded-md' />
        </form>
        <Select option={selectValue} onChange={(e: ChangeEvent<HTMLSelectElement>) => { set_media_file(e.target.value) }} />
      </div>
      <div className='fixed z-50 top-2.5 left-[225px]'>
        <button onClick={() => todani(1)} onDoubleClick={() => (lasan && set_media_show(-1))} className='sam bg-[#ff0] border-transparent border-2 font-bold py-1.5 px-2 rounded-md focus:border-red-500 focus:outline-none active:border-blue-600 active:bg-amber-200'>௰</button>
        <button onClick={() => todani(2)} onDoubleClick={() => (chalan && lasitam(false))} className='sam bg-[greenyellow] ml-4 border-transparent border-2 font-bold py-1.5 px-2 rounded-md focus:border-red-500 focus:outline-none active:border-blue-600 active:bg-lime-300'>௲</button>
      </div>
    </>
    <>
      {lasan && <div className={media_show ? '' : 'hidden'}>
        <TimeControl elm={media_ref} />
        {(() => {
          let dt = file[1]
          if (!lasan || dt[0] === '')
            return <></>
          let lc = window.localStorage.getItem("sthAnam") + "/" + dt[0]
          if (dt[2] === 0)
            return <audio ref={media_ref} id="media" controls loop autoPlay src={lc}></audio>
          else if (dt[2] === 1)
            return <video ref={media_ref} id="media" controls loop autoPlay src={lc}></video>
        })()}
      </div>}
    </>
    <Blink />
    <Nirdharanam />
  </div>
}

export default Home
const Select: NextPage<{ option: string, onChange: (e: ChangeEvent<HTMLSelectElement>) => void }> = ({ option, onChange }) => {
  const [list, setList] = useAtom(dattAMshState)
  useEffect(() => { // loading the File list
    if ('sthAnam' in window.localStorage) {
      loadData(window.localStorage.getItem('sthAnam') || '').then((v: datt_type) => {
        if (JSON.stringify(v) !== '{}')
          setList(v)
      })
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps
  let itemElm = Object.keys(list).map((val: string, index: number) =>
    <option key={index} value={val}>{list[val][1]} :- {val} {["🎵", "📀"][list[val][2]]}</option>
  )
  return <select value={option} onChange={onChange} className='w-5 h-4 mt-2 text-white bg-black outline-none border-2 rounded-sm border-gray-900' > {itemElm}</select>
}