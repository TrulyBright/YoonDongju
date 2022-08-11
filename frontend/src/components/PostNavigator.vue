<script>
export default {
  props: {
    text: String,
  },
  watch: {
    $route: {
      handler(newRoute) {
        document.title =
          "연세문학회 :: " +
          (newRoute.meta.breadCrumb === "function"
            ? this.text
            : newRoute.meta.breadCrumb[newRoute.meta.breadCrumb.length - 1]
                .text);
      },
      immediate: true,
    },
  },
};
</script>
<template>
  <nav aria-label="breadcrumb">
    <ol class="breadcrumb">
      <template
        v-for="stop in typeof $route.meta.breadCrumb === 'function'
          ? $route.meta.breadCrumb(text)
          : $route.meta.breadCrumb"
        :key="stop"
      >
        <RouterLink class="breadcrumb-item" :to="stop.to" v-if="'to' in stop">
          {{ stop.text }}</RouterLink
        >
        <li class="breadcrumb-item" v-else>{{ stop.text }}</li>
      </template>
    </ol>
  </nav>
</template>
<style></style>
