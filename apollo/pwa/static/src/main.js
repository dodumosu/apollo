import App from './App.svelte';

const app = new App({
    target: document.getElementById('app'),
    props: {
        endpoints: {
            list: '/api/forms',
            login: '/api/participants/login',
            logout: '/api/participants/logout',
            submit: '/api/submissions'
        }
    }
});

export default app;
