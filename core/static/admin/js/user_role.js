// Desmarcar checkboxes en tiempo real (JS)
document.addEventListener("DOMContentLoaded", function () {
  const roleField = document.getElementById("id_role");
  const staffField = document.getElementById("id_is_staff");
  const superuserField = document.getElementById("id_is_superuser");

  function toggleFields() {
    if (!roleField) return;
    const role = roleField.value;

    if (role === "cliente") {
      staffField.checked = false;
      staffField.disabled = true;
      superuserField.checked = false;
      superuserField.disabled = true;
    } else if (role === "admin") {
      staffField.disabled = false;
      staffField.checked = true;
      superuserField.checked = false;
      superuserField.disabled = true;
    } else {
      staffField.disabled = false;
      superuserField.disabled = false;
    }
  }

  roleField.addEventListener("change", toggleFields);
  toggleFields();
});
