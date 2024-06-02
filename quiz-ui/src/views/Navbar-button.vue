<template>
  <router-link :to="link">
    <button :style="{
      backgroundColor: backgroundColor,
      color: textColor,
      border: hasBorder ? '1px solid black' : 'none',
    }"
    class="navbar-button">
      {{ text }}
    </button>
  </router-link>
</template>

<script>
export default{
  name: 'NavbarButton',
  props: {
    backgroundColor: {
      type: String,
      required: true,
    },
    text: {
      type: String,
      required: true,
    },
    link: {
      type: String,
      required: true,
    },
    textColor: {
      type: String,
      default: 'white',
    },
    hasBorder: {
      type: Boolean,
      default: false,
    },
  }
}
</script>

<style scoped>
</style>