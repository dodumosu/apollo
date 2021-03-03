<script>
    export let field, locked, value = null;

    const optionSorter = (options_a, options_b) => options_b[0] - options_a[0];
    const options = Array.from(Object.entries(field.options)).sort(optionSorter);
</script>

<div class="mb-3">
    <label for={ field.tag } class="form-label"><span class="fw-bold">{ field.tag }</span> { field.description }</label>
    {#each options as [label, option_value], index}
        <div class="form-check">
            <label for={ `${field.tag}_${index}` } class="form-label">{ label }</label>
            <input type="radio" name={ field.tag } id={ `${field.tag}_${index}` } bind:group={ value } class="form-check-input" value={ option_value } disabled={ locked }>
        </div>
    {/each}
</div>