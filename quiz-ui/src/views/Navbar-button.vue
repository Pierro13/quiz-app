<template>
  <router-link :to="link">
    <button :style="{
      backgroundColor: hover ? backgroundColorHover : backgroundColor,
      color: textColor,
      // border : if hover is true and has border is true, then border none else border 1px solid black. If hover is false, then border 1px solid black
      border: hasBorder ? (hover ? 'none' : '1px solid black') : (hover ? '1px solid black' : 'none'),
    }"
    class="navbar-button"
    @mouseover="hover = true"
    @mouseout="hover = false"
    >
      {{ text }}
    </button>
  </router-link>
</template>

<script>
export default{
  name: 'NavbarButton',
  data(){
    return {
      hover: false,
    };
  },
  props: {
    backgroundColor: {
      type: String,
      required: true,
    },
    backgroundColorHover: {
      type: String,
      default: 'white',
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
button{
  width: 15vw;
  height: 8vh;
  font-weight: bold;
  font-size: 1.2em;
  cursor: pointer;
}
</style>