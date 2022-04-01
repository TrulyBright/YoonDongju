<script>
export default {
  props: {
    uuid: String,
    filename: String,
  },
};
</script>

<template>
  <div>
    <a :href="'/uploaded/' + uuid">{{ filename }}</a>
  </div>
</template>
