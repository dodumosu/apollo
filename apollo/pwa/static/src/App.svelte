<script>
    import gettext from 'gettext.js';
    import Notiflix from 'notiflix';
    import { getCookie } from 'tiny-cookie';

    import APIClient from './client';
    import LoginForm from './components/LoginForm.svelte';
    import UserInfo from './components/UserInfo.svelte';
    import LocalDatabase from './database';

    // ----- PROPS -----
    export let endpoints;

    let forms = [], participant = null, submissions = [];
    const apiClient = new APIClient(endpoints);
    const i18n = new gettext();
    const localDatabase = new LocalDatabase();


    // ----- EVENT HANDLERS -----
    const onAuthenticate = (event) => {
        Notiflix.Loading.Standard(i18n.gettext('Please wait'));
        apiClient.authenticate(event.detail.participant_id, event.detail.password)
            .then(result => {
                Notiflix.Loading.Remove();
                if (result.status === 200) {
                    result.payload.then(data => {
                        participant = data.data.participant;
                        participant.lastLogin = new Date();
                        localDatabase.saveParticipant(participant);
                    })
                } else {
                    Notiflix.Report.Failure(
                        i18n.gettext('Error'),
                        i18n.gettext('Please check your credentials and try again'),
                        i18n.gettext('OK')
                    );
                }
            })
            .catch(() => {
                Notiflix.Loading.Remove();
                Notiflix.Report.Failure(
                    i18n.gettext('Error'),
                    i18n.gettext('There was an error trying to log you in'),
                    i18n.gettext('OK')
                )
            });
    };

    const onLogout = () => {
        apiClient.logout(getCookie('crsf_access_token'))
            .then(() => {
                participant = null;
                forms = [];
                submissions = [];
            });
    };
</script>

<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top-mb-6">
    <div class="container-fluid"><a href="." class="navbar-brand">Apollo</a></div>
</nav>
<main class="container h-100">
    <div class="row h-75 align-items-center">
        <div class="col-sm-10 offset-sm-1 mt3">
            {#if participant === null}
                <LoginForm {i18n} on:authenticate={onAuthenticate}/>
            {:else}
                <UserInfo {i18n} {participant} pendingSubmissions={0} on:logout={onLogout}/>
            {/if}
        </div>
    </div>
</main>