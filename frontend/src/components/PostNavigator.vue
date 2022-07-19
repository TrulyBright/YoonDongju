<script>
export default {
  props: {
    text: String,
  }
}
</script>
<template>
  <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
      <template v-for="stop in typeof $route.meta.breadCrumb === 'function'
        ? $route.meta.breadCrumb(text)
        : $route.meta.breadCrumb" :key="stop">
        <RouterLink class="breadcrumb-item" :to="stop.to" v-if="'to' in stop">
          {{ stop.text }}</RouterLink
        >
        <li class="breadcrumb-item" v-else>{{ stop.text }}</li>
      </template>
    </ol>
  </nav>
</template>
<style></style>
