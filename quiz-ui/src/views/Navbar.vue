<!-- src/components/Navbar.vue -->
<template>
  <div class="container">
    <div class="left-part">
      <router-link to="/">
        <img src="@/assets/logo-code-master1.svg" alt="Logo" class="logo" width="55%" height="100%"/>
      </router-link>
    </div>
    <div class="right-part">
      <NavbarButton 
        backgroundColor="white" 
        backgroundColorHover="#ACECA1"
        text="Accueil" 
        link="/" 
        :hasBorder="true" 
        textColor="black" 
        class="welcome-button"
      />

      <NavbarButton
        backgroundColor = "white"
        backgroundColorHover = "#ACECA1"
        text="Scores"
        link="/scores"
        :hasBorder="true"
        textColor="black"
        class="scores-button"        
      />

      <NavbarButton 
        backgroundColor="#ACECA1" 
        text="Administrateur" 
        link="/admin" 
        :hasBorder="false" 
        textColor="black" 
        class="admin-button"
        />
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
  }

  .left-part{
    margin-top: 1vh;
    margin-left: 1vw;
  }

  .right-part{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 50%;
    margin-right: 3vw;
  }

</style>
