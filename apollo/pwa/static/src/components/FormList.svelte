<script>
    import { createEventDispatcher } from 'svelte';
    export let forms, i18n;

    const dispatch = createEventDispatcher();

    const getActionLabel = form => form.form_type === 'CHECKLIST' ? i18n.gettext('Edit') : i18n.gettext('Create');

    const formActionHandler = form => {
        dispatch('form-action', {
            form: form
        });
    };
</script>

<div class="row mt-3">
    <div class="col">
        <div class="card shadow-sm">
            <h5 class="card-header">{ i18n.gettext('Forms') }</h5>
            <div class="list-group list-group-flush">
                {#each forms as form}
                    <div class="list-group-item">
                        <div class="row">
                            <div class="col mb-2">{ form.name }</div>
                        </div>
                        <div class="row">
                            <div class="col mb-2"><span class="badge bg-secondary">{ form.form_type }</span></div>
                        </div>
                        <div class="row">
                            <div class="col">
                                <button class="btn btn-outline-dark float-end" on:click={formActionHandler(form)}>{ getActionLabel(form) }</button>
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>