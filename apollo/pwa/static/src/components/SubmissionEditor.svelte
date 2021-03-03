<script>
    import { createEventDispatcher } from 'svelte';

    import CommentField from './form-fields/CommentField.svelte';
    import ImageField from './form-fields/ImageField.svelte';
    import IntegerField from './form-fields/IntegerField.svelte';
    import LocationField from './form-fields/LocationField.svelte';
    import MultiSelectField from './form-fields/MultiSelectField.svelte';
    import SelectField from './form-fields/SelectField.svelte';
    import StringField from './form-fields/StringField.svelte';

    export let form, i18n, submission;
    let locked = form.form_type === 'INCIDENT' && submission.posted;

    const dispatch = createEventDispatcher();

    const buttonHandler = () => {
        dispatch('submission-updated', {submission: submission});
    };
</script>

<div class="row">
    <div class="col">
        <div class="card shadow-sm">
            <h5 class="card-header">{ form.name }</h5>
            <div class="card-body">
                <form>
                    {#if form.form_type === 'SURVEY'}
                    <fieldset>
                        <div class="mb-3">
                            <label for="serial" class="form-label">{ i18n.gettext('Serial number') }</label>
                            <input class="form-control" name="serial" id="serial">
                        </div>
                    </fieldset>
                    {/if}
                    {#each form.data.groups as group}
                        <fieldset>
                            <legend>{ group.name }</legend>
                            {#each group.fields as field}
                                {#if field.type === 'integer'}
                                    <IntegerField {field} {locked} bind:value={submission.data[field.tag]}/>
                                {:else if field.type === 'select'}
                                    <SelectField {field} {locked} bind:value={submission.data[field.tag]}/>
                                {:else if field.type === 'multiselect'}
                                    <MultiSelectField {field} {locked} bind:value={submission.data[field.tag]}/>
                                {:else if field.type === 'string'}
                                    <StringField {field} {locked} bind:value={submission.data[field.tag]}/>
                                {:else if field.type === 'comment'}
                                    <CommentField {field} {locked} bind:value={submission.data[field.tag]}/>
                                {:else if field.type === 'image'}
                                    <ImageField {field} {locked} bind:value={submission.data[field.tag]}/>
                                {/if}
                            {/each}
                        </fieldset>
                    {/each}
                    {#if 'geolocation' in navigator}
                        <LocationField {i18n} bind:location={submission.location} {locked} />
                    {/if}
                </form>
            </div>
            <div class="card-footer">
                <button class="btn btn-outline-dark" on:click={buttonHandler}>{ i18n.gettext('Back') }</button>
                <button class="btn btn-outline-dark" on:click={buttonHandler}>{ i18n.gettext('Cancel') }</button>
                <button class="btn btn-outline-dark" on:click={buttonHandler}>{ i18n.gettext('Submit') }</button>
            </div>
        </div>
    </div>
</div>