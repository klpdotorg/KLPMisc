var schoolid;
var handle;
var cal1;
var type;

function initCap(str)
{
  str = str.substring(0,1).toUpperCase() + str.substring(1,str.length).toLowerCase();
 return str;
}


function isNumeric(str)
{
  if (!(/^\d*$/.test(str.value)))
  {
    alert(str.id+" should only be numeric");
    str.value="";
    str.focus();
    return false;
  }
  return true;
}

function textCounter(field,cntfield,maxlimit) {
  if (field.value.length > maxlimit) // if too long...trim it!
    field.value = field.value.substring(0, maxlimit);
  // otherwise, update 'characters left' counter
  else
    cntfield.value = maxlimit - field.value.length;
}


function editText(sysid)
{
  document.getElementById(sysid+"-comments").disabled=false;
  document.getElementById(sysid+"-comments").readOnly=false;
}


function disableForm(theform)
{
  for (i = 0; i < theform.length; i++) {
    var tempobj = theform.elements[i];
    if (tempobj.type.toLowerCase() == "button" || tempobj.type.toLowerCase() == "submit")
      tempobj.disabled = true;
  }
  return true;
}

function submitData(sysid,type,theform)
{
  var columnValues = [];
  if (type == "verify")
  {
    document.getElementById(sysid+"_verified").disabled=true;
  }
  else
    document.getElementById(sysid+"_rejected").disabled=true;
  for (i = 0; i < theform.length; i++) {
    var tempobj = theform.elements[i];
    if (tempobj.type.toLowerCase() == "button" || tempobj.type.toLowerCase() == "submit")
      tempobj.disabled = true;
  }
 return true;
}


function postData()
{
  var form = document.createElement("form");
  form=document.forms['story'];
  form.setAttribute("method", "post");
  form.setAttribute("action", "/postSYS/"+schoolType);
  var result = form.submit();
}
