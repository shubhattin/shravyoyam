import type { NextPage } from 'next'
import { useAtomValue } from 'jotai'
import { blinkState } from 'state'
const Blink: NextPage = () => {
    const blink_sthiti = useAtomValue(blinkState)
    return <>
        <div className={`bg-white w-8 h-8 fixed left-5 bottom-6 rounded-2xl ${blink_sthiti ? '' : 'hidden'}`}></div>
    </>;
}
export default Blink;