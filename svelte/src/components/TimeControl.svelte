<script lang="ts">
  import { currentTime } from '@store/index';

  let tm = [0, 0, 0]; // seconds, minutes, hours
  let tm_show = false;

  const hide_show = () => (tm_show = !tm_show);
  const load_current = () => {
    let dur = $currentTime;
    let sec = dur % 60;
    dur -= sec;
    dur /= 60;
    sec = Math.trunc(sec);
    let min = dur % 60;
    dur -= min;
    dur /= 60;
    let hrs = dur % 60;
    tm = [sec, min, hrs];
  };
  const set_current = () => {
    let t = tm[0];
    t += tm[1] * 60;
    t += tm[2] * 3600;
    $currentTime = t;
  };
  const lower_time = () => {
    $currentTime -= 10;
    load_current();
  };
  const higher_time = () => {
    $currentTime += 10;
    load_current();
  };
</script>

<div class="mb-2.5 mt-4">
  <button
    on:click={hide_show}
    class={`text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-green-300 active:border-green-500 ${
      !tm_show ? '' : 'hidden'
    }`}
  >
    Show
  </button>
  <button
    on:click={hide_show}
    class={`text-white p-1 border-2 border-yellow-400 m-1 rounded-md active:text-red-300 active:border-red-500 ${
      tm_show ? '' : 'hidden'
    }`}
  >
    Hide
  </button>
</div>
<div class={`mb-2.5 mt-5 ${tm_show ? '' : 'hidden'}`}>
  <button
    on:click={lower_time}
    class="text-2xl text-white font-bold border-2 rounded-lg p-[3px] active:text-red-300 active:border-red-400"
  >
    -
  </button>
  <span>
    <input
      type="number"
      bind:value={tm[2]}
      class="w-10 border-2 border-yellow-200 text-green-300 bg-black font-medium m-2 rounded"
    />
    <span class="font-semibold text-2xl text-white">:</span>
    <input
      type="number"
      bind:value={tm[1]}
      class="w-10 border-2 border-yellow-200 text-green-300 bg-black font-medium m-2 rounded"
    />
    <span class="font-semibold text-2xl text-white">:</span>
    <input
      type="number"
      bind:value={tm[0]}
      class="w-10 border-2 border-yellow-200 text-green-300 bg-black font-medium m-2 rounded"
    />
  </span>
  <button
    on:click={higher_time}
    class="text-2xl text-white font-bold border-2 rounded-lg p-[3px] active:text-green-300 active:border-green-400"
  >
    +
  </button>
  <div class="mt-3">
    <button
      on:click={load_current}
      class="text-white p-1 border-2 border-red-400 m-1 rounded-md active:text-yellow-500 active:border-blue-500"
    >
      Load
    </button>
    <button
      on:click={set_current}
      class="text-white p-1 border-2 border-red-400 m-1 rounded-md active:text-yellow-500 active:border-blue-500"
    >
      Set
    </button>
  </div>
</div>
