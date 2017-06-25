//全局基础方法封装
function skyAjax(url,req,Data,successfn, errorfn){
		$.ajax({
			url:url,
			type:req,
			dataType:'json',
			data:Data,
			success: function(d){
                successfn(d);
            },
            error: function(e){
                errorfn(e);
            }
		})
	}

// 删除操作的方法封装
function delete_opt(id, text, url){

    if(confirm(text)){
           skyAjax(url+id,'post',{},function(data){
                    if(data.code==200){
                        location.reload();
                    }else{
                        alert('delete failed')
                    }

			    },function(e){
			        alert(e.message);
			    });
    }
}

// 删除应用
function delete_applications(id){
    delete_opt(id, "delete this application?", delete_application)
}

// 删除数据
function delete_data(id){
    delete_opt(id, "delete this data?", delete_datafile)
}

// 删除任务
function delete_jobs(id){
    delete_opt(id, "delete this job?", delete_job)
}


