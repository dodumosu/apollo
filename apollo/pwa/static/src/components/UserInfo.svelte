<script>
    import {createEventDispatcher} from 'svelte';

    const dispatch = createEventDispatcher();

    export let i18n, participant, pendingSubmissions;

    const greeting = () => {
        let hourOfDay = new Date().getHours();
        if (hourOfDay < 12)
            return i18n.gettext('Good morning');
        else if (12 >= hourOfDay && hourOfDay < 17)
            return i18n.gettext('Good afternoon');
        else
            return i18n.gettext('Good evening');
    };

    const handleLogout = () => {
        dispatch('logout');
    };
</script>

<div class="row">
    <div class="col">
        <div class="card shadow-sm">
            <div class="card-body">
                <h5 class="card-title">{ greeting() }, { participant.full_name }</h5>
                <div class="row mb-3">
                    <div class="col-4"><strong>{ i18n.gettext('Participant ID') }</strong></div>
                    <div class="col">{ participant.participant_id }</div>
                </div>
                <div class="row mb-3">
                    <div class="col-4"><strong>{ i18n.gettext('Location') }</strong></div>
                    <div class="col">{ participant.location }</div>
                </div>
                <div class="row mb-3">
                    <div class="col"><button class="btn btn-outline-dark" on:click={handleLogout}>{ i18n.gettext('Click here') }</button> { i18n.gettext('if this is not you.') }</div>
                </div>
                {#if pendingSubmissions && pendingSubmissions > 0 }
                    <div class="row">
                        <div class="col">
                            <div class="alert alert-info">{ i18n.gettext('Pending submissions:') } <strong>{ pendingSubmissions }</strong></div>
                        </div>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>