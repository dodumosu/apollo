<script>
    export let field, locked, value = null;
</script>

<div class="mb-3">
    <label for={ field.tag } class="form-label"><span class="fw-bold">{ field.tag }</span> { field.description }</label>
    <textarea name={field.tag} id={field.tag} cols="30" rows="10" class="form-control" disabled={locked} bind:value></textarea>
</div>