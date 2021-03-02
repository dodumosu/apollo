<script>
    export let field, locked, value;
</script>

<div class="mb-3">
    <label for={ field.tag } class="form-label"><span class="fw-bold">{ field.tag }</span> { field.description }</label>
    <input type="text" name={ field.tag } id={ field.tag } class="form-control" disabled={locked} bind:value>
</div>