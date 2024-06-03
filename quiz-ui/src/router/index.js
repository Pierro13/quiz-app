import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import ScoresView from '@/views/ScoresView.vue';
import QuestionsManger from '@/views/QuestionsManager.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'new-quiz',
      component: NewQuizPage,
    },
    {
      path: '/scores',
      name: 'scores',
      component: ScoresView,
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsManger,
    }
  ]
});

export default router;
