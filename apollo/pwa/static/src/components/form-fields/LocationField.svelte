<script>
    import Notiflix from 'notiflix';
    import { createEventDispatcher } from 'svelte';

    export let location = null, i18n, locked;

    const dispatch = createEventDispatcher();
    const getCoordinates = (loc) => {
        if (loc)
            return loc;
        
        return [i18n.gettext('N/A'), i18n.gettext('N/A')];
    }

    const getLocationHandler = () => {
        navigator.geolocation.getCurrentPosition(position => {
            location = [position.coords.longitude, position.coords.latitude];

        },
        () => {
            Notiflix.Report.Failure(
                i18n.gettext('Error'),
                i18n.gettext('There was an error retreiving your location'),
                i18n.gettext('OK')
            )
        })
    };
</script>

<fieldset>
    <legend>{ i18n.gettext('Location') }</legend>
    <div class="mb-3">
        <pre>({ getCoordinates(location)[1] }, { getCoordinates(location)[0] })</pre>
        <button type="button" class="btn btn-outline-dark" disabled={locked} on:click={getLocationHandler}>{ i18n.gettext('Get location') }</button>
    </div>
</fieldset>