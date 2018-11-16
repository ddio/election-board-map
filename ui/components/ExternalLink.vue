<template lang="pug">
  a(:href="to" target="_blank" rel="noopener noreferrer")
    slot
</template>
<script>
export default {
  props: {
    to: {
      type: String,
      required: true
    }
  }
}
</script>

