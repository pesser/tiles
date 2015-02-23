var get_data_for_title = function(){
  data = ${json_data};
  var data_getter = function(title){
    for(var entry in data){
      if(data[entry]["Title"] == title){
        return data[entry]
      }
    }
  }
  return data_getter
}()
