document.getElementById("checkbox").addEventListener("change", function(){
    const hiddenrole = document.getElementById("hiddenRole");
    hiddenrole.value = this.checked ? "worker":"user";
});//функция для выбора пользователя

