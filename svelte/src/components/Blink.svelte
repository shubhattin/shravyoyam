<script lang="ts">
  import { blinking } from '@store/index';
  $: {
    if ($blinking) {
      setTimeout(() => blinking.set(false), 400);
    }
  }
</script>

<div class={`bg-white w-8 h-8 fixed left-5 bottom-6 rounded-2xl ${$blinking ? '' : 'hidden'}`} />
