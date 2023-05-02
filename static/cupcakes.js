
$('.delete-cupcake').click(deleteCupcake)
async function deleteCupcake() {
  const id = $(this).data('id')
  await axios.delete(`/api/cupcakes/${id}`)
  $(this).parent().remove()
};


$("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();

    let data = {
      flavor: $("#form-flavor").val(),
      rating: $("#form-rating").val(),
      size: $("#form-size").val(),
      image: $("#form-image").val()
    };

    const res = await axios.post("http://127.0.0.1:5000/api/cupcakes", data);

    $("#new-cupcake-form").trigger("reset");
    location.reload();
  });