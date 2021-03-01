<script>
    import gettext from 'gettext.js';
    import Notiflix from 'notiflix';
    import { onMount } from 'svelte/internal';
    import { getCookie } from 'tiny-cookie';

    import APIClient from './client';
    import FormList from './components/FormList.svelte';
    import LoginForm from './components/LoginForm.svelte';
    import UserInfo from './components/UserInfo.svelte';
    import LocalDatabase from './database';

    // ----- UTILITIES -----
    const formSorter = (a, b) => {
        const FORM_TYPE_MAP = {
            CHECKLIST: 1,
            SURVEY: 2,
            INCIDENT: 3
        };

        if (a.form_type !== b.form_type)
            return FORM_TYPE_MAP[a.form_type] - FORM_TYPE_MAP[b.form_type];
        
        if (a.name === b.name)
            return a.id - b.id;
        
        if (a.name < b.name)
            return -1;
        else
            return 1;
    };

    const refreshForms = async (participant) => {
        let result = await apiClient.getForms(participant.events);
        let data = await result.payload;
        
        return data.objects.map(
            form => Object.assign(
                {}, form, {participant_id: participant.participant_id}
            )
        ).sort(formSorter); 
    };

    // ----- PROPS -----
    export let endpoints;

    let forms = [], participant = null, submissions = [];
    const apiClient = new APIClient(endpoints);
    const i18n = new gettext();
    const localDatabase = new LocalDatabase();

    // ----- EVENT HANDLERS -----
    const onAuthenticate = async (event) => {
        Notiflix.Loading.Standard(i18n.gettext('Please wait'));
        try {
            let result = await apiClient.authenticate(event.detail.participant_id, event.detail.password);
            Notiflix.Loading.Remove();

            if (result.status === 200) {
                let data = await result.payload;
                participant = data.data.participant;
                participant.lastLogin = new Date();
                localDatabase.saveParticipant(participant);

                // get forms
                try {
                    forms = await refreshForms(participant);
                    localDatabase.saveForms(forms);
                } catch (error) {
                    console.error(error);
                    Notiflix.Report.Failure(
                        i18n.gettext('Error'),
                        i18n.gettext('There was an error loading forms'),
                        i18n.gettext('OK')
                    );
                }
            } else {
                Notiflix.Report.Failure(
                    i18n.gettext('Error'),
                    i18n.gettext('Please check your credentials and try again'),
                    i18n.gettext('OK')
                );
            }
        } catch (error) {
            Notiflix.Loading.Remove();
            Notiflix.Report.Failure(
                i18n.gettext('Error'),
                i18n.gettext('There was an error trying to log you in'),
                i18n.gettext('OK')
            )
        }
    };

    const onLogout = () => {
        apiClient.logout(getCookie('csrf_access_token'))
            .then(() => {
                participant = null;
                forms = [];
                submissions = [];
            });
    };

    const onAppMount = async () => {
        participant = await localDatabase.getParticipant();
        if (participant !== null) {
            let dbForms = await localDatabase.getForms(participant.participant_id);
            forms = dbForms.sort(formSorter);
            submissions = await localDatabase.getSubmissions(participant.participant_id);
        }
    };


    onMount(onAppMount);
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
                <FormList {i18n} {forms}/>
            {/if}
        </div>
    </div>
</main>