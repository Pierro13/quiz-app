<!-- src/components/Navbar.vue -->
<template>
  <div class="container">
    <div class="left-part">
      <img src="@/assets/logo-code-master1.svg" alt="Logo" class="logo" width="55%" height="100%"/>
    </div>
    <div class="right-part">
      <NavbarButton backgroundColor="white" text="Accueil" link="/" hasBorder="true" textColor="black"/>
      <NavbarButton backgroundColor="#ACECA1" text="Administrateur" link="/new-quiz" hasBorder="false" textColor="black"/>
    </div>
  </div>
</template>

<script>
import NavbarButton from '@/views/Navbar-button.vue';
export default {
  name: 'Nav-bar',
  components: {
    NavbarButton,
  } 
}
</script>

<style scoped>
  .container{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid black;
  }

  .logo{
    
  }
</style>
