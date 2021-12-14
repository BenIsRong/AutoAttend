$(function(){
    $.ajax(
        {
            method: "get",
            url: "/api/v1/students"
        }
    ).done(
        (data)=>{
            data = JSON.parse(data);
            data["students"].forEach((student)=>{
                $("#students_table").append(`
                    <tr>
                        <td>${student.reg}</td>
                        <td>${student.name}</td>
                        <td>${student.class}</td>
                        <td><a onclick="confirm_delete_student('${student.id}', '${student.personId}', '${student.name}')" href="">remove ${student.name}</a></td>
                        <td><a href="/editStudent?id=${student.id}">edit ${student.name}</a></td>
                    </tr>
                `);
            });
        }
    ).fail(
        (err)=>{
            console.log(err.responseText);
        }
    );

    $.ajax(
        {
            method: "get",
            url: "/api/v1/records"
        }
    ).done(
        (data)=>{
            data = JSON.parse(data);
            data["records"].forEach((record)=>{
                $("#records_table").append(`
                    <tr>
                        <td>${record.reg}</td>
                        <td>${record.name}</td>
                        <td>${record.date}</td>
                        <td>${record.time}</td>
                        <td><a onclick="confirm_delete_attendance('${record.id}', '${record.name}')" href="">remove attendance</a></td>
                        <td><a href="/editAttendance?id=${record.id}">edit attendance</a></td>
                    </tr>
                `);
            });
        }
    ).fail(

    );
});

function confirm_delete_student(id, personId, name){
    if(window.confirm(`are you sure you want to delete ${name}'s record?`)){
        $.ajax(
            {
                method: "delete",
                url: "/api/v1/students",
                data: {
                    id: id,
                    personId
                }
            }
        ).done(
            (data)=>{
                location.reload();
            }
        ).fail(
            (err)=>{
                console.log(err.responseText);
            }
        );
    }
}

function confirm_delete_attendance(id, name){
    if(window.confirm(`are you sure you want to delete ${name}'s attendance?`)){
        $.ajax(
            {
                method: "delete",
                url: "/api/v1/records",
                data: {
                    id: id
                }
            }
        ).done(
            (data)=>{
                location.reload();
            }
        ).fail(
            (err)=>{
                console.log(err.responseText);
            }
        );
    }
}

function show_image(file){
    console.log(file);
    var file_reader = new FileReader();
    
    file_reader.onload = (event)=>{
        $("#attendance_image").attr('src', event.target.result);
    };

    file_reader.readAsDataURL(file.files[0]);
}