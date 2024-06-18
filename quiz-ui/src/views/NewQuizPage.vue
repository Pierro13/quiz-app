<template>
  <div class="global-container">
    <div class="container">
    <div class="input-holder">
      <h3>Saisissez votre nom</h3>
      <input type="text" placeholder="Username" v-model="username" />
      <button @click="launchNewQuiz">GO!</button>
    </div>
  </div>
  </div>
</template>

<script setup>
  import ParticipationStorageService from '@/services/ParticipationStorageService';
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';

  let username = ref('');
  const router = useRouter();

  function launchNewQuiz() {
    if(username.value){
      ParticipationStorageService.savePlayerName(username.value);
      router.push('/questions');
      console.log("Launch new quiz with", username.value);
    }
    else{
      alert("Please enter your name.");
    }    
  }
</script>

<style scoped>
  .global-container{
    display: flex;
    justify-content: center;
  }

  .container{
    margin-top: 10vh;
    border-radius: 10px;
    background-color: #ACECA1;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 30vw;
    padding-bottom: 3vh;
  }
</style>
