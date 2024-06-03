<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
    console.log("Home page mounted");
    try {
        const response = await quizApiService.getQuizInfo();
        console.log("Scores récupérés : ", response.scores); // Log the scores
        registeredScores.value = response.scores; // Assign the scores array
    } catch (error) {
        console.error("Erreur lors de la récupération des scores : ", error);
    }
});
</script>

<template>
  <!-- <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    <p>{{ scoreEntry.date }} - {{ scoreEntry.score }}</p>
  </div>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link> -->
  <div class="container">
    <div class="left-part">
      <h1>Testez et améliorez vos compétences <a href="/new-quiz" class="green-underline-text">en jouant</a></h1>
      <p>Plongez dans l'univers passionnant de la programmation avec notre site de quiz interactifs conçu spécialement pour les développeurs de tous niveaux.</p>
    </div>
    <div class="right-part">
      <img class="homepage" src="@/assets/logo-code-master1.svg" alt="Logo" width="55%" height="100%"/>
      <a class="play-button" href="/new-quiz">Jouer</a>
      <a class="play-button" href="/scores">Voir les scores</a>
    </div>
  </div>
</template>

<style scoped>
  .container{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .left-part{
    width: 50%;
    margin: 5vh 1vw 0 3vw;
  }

  .right-part{
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  h1{
    font-size: 5em;
    margin-left: 1vw;
  }

  p{
    font-size: 1.5em;
    margin-left: 1vw;
  }

  .green-underline-text{
    color: #06D610;
    text-decoration: underline;
    cursor: pointer;
  }

  .green-underline-text:active{
    color: #ACECA1;
  }

  .play-button{
    width: 20vw;
    height: 10vh;
    font-weight: bold;
    font-size: 1.2em;
    cursor: pointer;
    background-color: #ACECA1;
    border: none;
    text-align: center;
    text-decoration: none;
    align-items: center;
    display: flex;
    justify-content: center;
    color: inherit;
    margin-bottom: 4vh;
  }

  .right-part img{
    margin-bottom: 10vh;
    margin-top: 10vh;
  }

  .play-button:hover{
    background-color: #06D610;
  }
</style>
