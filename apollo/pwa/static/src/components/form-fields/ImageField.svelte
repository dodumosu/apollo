<script>
    import Compressor from 'compressorjs';

    export let field, locked, value = null;

    const processFile = event => {
        const imageFile = event.target.files[0];

        if (!imageFile)
            return;
        
        
    };

    const resizeImage = image => {};
</script>

<div class="mb-3">
    <div class="card"><img src="" alt="" class="card-img-top" width="320"></div>
    <label for={field.tag} class="form-label"><span class="fw-bold">{ field.tag}</span> { field.description }</label>
    <input type="file" name={field.tag} id={field.tag} class="form-control" accept="image/*" disabled={locked} on:change={processFile}>
</div>