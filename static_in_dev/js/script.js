jQuery(document).ready(function() {
    var maxHeight = 0;

    $(".answer").each(function() {
        if ($(this).height() > maxHeight) {
            maxHeight = $(this).height();
        }
    });

    $(".answer").height(maxHeight);

    $("#profile_success").fadeOut(4000);

    var cw = $(".profile-pic").width();
    $(".profile-pic").css({"height":cw+"px"});

    $("#changeImg").click(function(){
        $(".profile-image-input").click();
    });

    $(".profile-image-input").on("change", function(){
        $(".profile_form").submit();
    });

    $("#img_wrapper").click(function(){
        $(".image-input").click();
    });

    $(".image-input").on("change", function(){
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf(".") + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg"))
        {
            var reader = new FileReader();

            reader.onload = function (e) {
                $("#quiz_img").attr("src", e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    });

    var q_count = 1;
    var a_count = [4];

    function addAnswerBlock(obj, ind){
        if (a_count[ind-1] < 6) {
            a_count[ind-1] += 1;
            var tmp = $("#a_example").clone();
            tmp.find(".prep").html("A" + a_count[ind-1]);

            tmp.attr("id", "");

            obj.append(tmp);
        }
    }

    function delAnswerBlock(obj, ind) {
        if (a_count[ind-1] > 2) {
            a_count[ind-1] -= 1;
            obj.find(".input-group:last").remove();
        }
    }

    $("#question_add").click(function(){
        var tmp = $("#q_example").clone();
        q_count += 1;
        var text = "#" + q_count + " Question:";
        tmp.children("h3").html(text);

        tmp.find(".add_a_btn").attr("ind", q_count).on("click", function() {
            var target = $(this).closest("div").siblings(".a_area");
            var ind = $(this).attr("ind");
            addAnswerBlock($(target), ind);
        });

        tmp.find(".del_a_btn").attr("ind", q_count).on("click", function() {
            var target = $(this).closest("div").siblings(".a_area");
            var ind = $(this).attr("ind");
            delAnswerBlock($(target), ind);
        });

        a_count.push(tmp.find("[name *= a]").length);

        $(".questions-add-block").append(tmp);
    });

    $(".add_a_btn").click(function(){
        var target = $(this).closest("div").siblings(".a_area");
        var ind = $(this).attr("ind");
        addAnswerBlock($(target), ind);
    });

    $(".del_a_btn").click(function(){
        var target = $(this).closest("div").siblings(".a_area");
        var ind = $(this).attr("ind");
        delAnswerBlock($(target), ind);
    });

    $("#send_quiz").click(function(){
        var json_quiz = new Object();
        json_quiz.quiz_title = $("#quiz_title").val();
        json_quiz.quiz_description = $("#quiz_desc").val();
        json_quiz.questions = [];
        $(".question-add").each(function(index){
            if (index == 0){
                return;
            }
            json_quiz.questions.push(new Object());
            var lst_ind = json_quiz.questions.length - 1;
            json_quiz.questions[lst_ind].question = $(this).find("[name *= q]").val();
            json_quiz.questions[lst_ind].answers = [];
            json_quiz.questions[lst_ind].correct = [];

            $(this).find("[name *= a]").each(function(){
                json_quiz.questions[lst_ind].answers.push($(this).val());
            });

            var i = 0;

            $(this).find("[name *= c]").each(function(){
                if ($(this).is(":checked"))
                {
                    json_quiz.questions[lst_ind].correct.push(i);
                }
                i++;
            });
        });
        var jsonString= JSON.stringify(json_quiz);
        $("#post_form").find("[name = json_data]").attr("value", jsonString);
        $("#post_form").submit();
    });

    $(".like-btn").click(function(){
        like_cnt = $(this).next(".like_cnt")
        like_btn = $(this)
        $.get("/quizz/like/", {id: $(this).attr("qid")}, function(data){
            likes = parseInt(like_cnt.html());
            if (data == "True"){
                likes += 1;
                like_btn.toggleClass("liked");
            }
            else{
                likes -= 1;
                like_btn.toggleClass("liked");
            }
            like_cnt.html(likes);
        });
    });

    $("#show_more").click(function(){
        var btn_obj = this;
        var next_page = $(this).attr("next_pg");

        $.get("/quizz/get_next_page/", {next: next_page}, function(data){
            if (data == "False"){

            }else{
                $("#all_bl").append(data);
                console.log($(btn_obj).attr("next_pg"));
                $(btn_obj).attr("next_pg", ++next_page);
            }
        });
    });

    $("#search_input").on("input", function(){
        var query = $(this).val();
        var block = this
        if(query.trim()){
            $("#show_more").hide();
        }else{
            $("#show_more").show();
        }

        $.get("/quizz/search/", {query: query}, function(data){
            $("#all_bl").html(data);
        });
    });

    $("#search_form").on("submit", function(){
        return false;
    });

    document.querySelectorAll("#hide_btn").forEach(
        item => item.addEventListener("click", function() {
            var block_id = "#" + $(this).attr("to")
            if ($(block_id).css("display").toLowerCase() == "flex"){
                $(block_id).hide(300);
                $(this).html("Show");
            }else{
                $(block_id).show(300);
                $(this).html("Hide");
            }
        })
    );
});
