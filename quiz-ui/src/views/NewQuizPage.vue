<template>
  <h1>New Quiz Page Works !</h1>
  <div class="container">
    <h3>Saisissez votre nom</h3>
    <input type="text" placeholder="Username" v-model="username" />
    <button @click="launchNewQuiz">GO!</button>
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
