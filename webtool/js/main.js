$(function(){

    var dataJson = function(){
		
		var pointdata = []
		for (var i = 0; i < points.length; i++) {
	        pointdata.push(points[i].x, 500-points[i].y);
		};
		var reduce_rate = [];
		$.each($('input[name="reduce_rate"]') ,function(index,domEle){
			reduce_rate.push(domEle.value);
		});
		var tolerance_of_edge_length = [];
		$.each($('input[name="tolerance_of_edge_length"]') ,function(index,domEle){
			tolerance_of_edge_length.push(domEle.value);
		});
		var length_constraint_maltiplier = [];
		$.each($('input[name="length_constraint_maltiplier"]') ,function(index,domEle){
			length_constraint_maltiplier.push(domEle.value);
		});
		var boundary_constraint_magnitude = [];
		$.each($('input[name="boundary_constraint_magnitude"]') ,function(index,domEle){
			boundary_constraint_magnitude.push(domEle.value);
		});
		var perp_steps = [];
		$.each($('input[name="perp_steps"]') ,function(index,domEle){
			perp_steps.push(domEle.value);
		});
		var minumum_radius = [];
		$.each($('input[name="minumum_radius"]') ,function(index,domEle){
			minumum_radius.push(domEle.value);
		});
		var maximum_radius = [];
		$.each($('input[name="maximum_radius"]') ,function(index,domEle){
			maximum_radius.push(domEle.value);
		});

		return {
			'pointdata' : pointdata,
			'reduce_rate' : reduce_rate,
			'tolerance_of_edge_length' : tolerance_of_edge_length,
			'length_constraint_maltiplier' : length_constraint_maltiplier,
			'boundary_constraint_magnitude' : boundary_constraint_magnitude,
			'perp_steps' : perp_steps,
			'minumum_radius' : minumum_radius,
			'maximum_radius' : maximum_radius
		};
    };
	
	$("#btn_submit").click(function(){
        var obj = dataJson();
        //这里不会啦。。。怎么post过去啊。。。
    });
})

document.getElementById("reduce_rate").defaultValue = "0.5";
document.getElementById("tolerance_of_edge_length").defaultValue = "0.3";
document.getElementById("length_constraint_maltiplier").defaultValue = "0.5";
document.getElementById("boundary_constraint_magnitude").defaultValue = "5";
document.getElementById("perp_steps").defaultValue = "10000";
document.getElementById("minumum_radius").defaultValue = "1";
document.getElementById("maximum_radius").defaultValue = "10";

const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');

//线段的点的集合
var points=[];
//可拖动圆圈的点的集合
var circles=[];
//每一个点的对象
var isDragging=false
function Point(x, y) {
    this.x = x;
    this.y = y;
}
//圆圈对象
function Circle(x, y) {
     this.x = x;
     this.y = y;
     this.radius = 10;
     this.color = "blue";
     //拖拽点的标记
     this.isSelected = false;
}
  
var point=new Point(50,50);
points.push(point);
var point=new Point(450,250);
points.push(point);
var point=new Point(450,350);
points.push(point);
var point=new Point(200,225);
points.push(point);
var point=new Point(50,200);
points.push(point);
var circle=new Circle(50,50);
circles.push(circle);
var circle=new Circle(450,250);
circles.push(circle);
var circle=new Circle(450,350);
circles.push(circle);
var circle=new Circle(200,225);
circles.push(circle);
var circle=new Circle(50,200);
circles.push(circle);

//进入下面的代码，绘制点
context.clearRect(0,0,canvas.width,canvas.height);
//遍历数组画圆
circles[0].color="blue";
for(var i=0; i<circles.length; i++) {
	var circle = circles[i];
	// 绘制圆圈
	context.globalAlpha = 0.85;
	context.beginPath();
	context.arc(circle.x, circle.y, circle.radius, 0, Math.PI*2);
	context.fillStyle = circle.color;
	context.strokeStyle = "black";
	context.fill();
	context.stroke();
 }
// 画线
context.beginPath();
context.lineWidth = 4;
//从起始点开始绘制
context.moveTo(points[0].x,points[0].y);
for (var i = 0; i < points.length; i++) {
	context.lineTo(points[i].x, points[i].y);
}
context.lineTo(points[4].x, points[0].y);
context.fillStyle="rgb(128,128,128)";
context.fill();
context.strokeStyle="black";
context.stroke();

canvas.onmousedown=function(e){
    var clickX = e.pageX - canvas.offsetLeft;
    var clickY = e.pageY - canvas.offsetTop;
    //判断当前点击点是否在已经绘制的圆圈上，如果是执行相关操作，并return，不进入画线的代码
    for(var i=1; i<circles.length; i++) {
        var circle = circles[i];
        //使用勾股定理计算这个点与圆心之间的距离
        var distanceFromCenter = Math.sqrt(Math.pow(circle.x - clickX, 2) + Math.pow(circle.y - clickY, 2));
        // 如果是其他的点，则设置可以拖动
        if (distanceFromCenter <= circle.radius) {
            // 清除之前选择的圆圈
            index=i;
            isDragging=true;
            //停止搜索
            return;
        }
    }
};
   
canvas.onmousemove=function(e){
   // 判断圆圈是否开始拖拽
   if (isDragging == true) {
        // 判断拖拽对象是否存在
        // 取得鼠标位置
        var x1 = e.pageX - canvas.offsetLeft;
        var y1 = e.pageY - canvas.offsetTop;
        context.clearRect(0,0,canvas.width,canvas.height);
        //根据上文得到的index设置index点位置随鼠标改变
        circles[index].x=x1;
        circles[index].y=y1;
        points[index].x=x1;
        points[index].y=y1;
        for(var i=0; i<circles.length; i++) {
            var circle = circles[i];
            // 绘制圆圈
            context.globalAlpha = 0.85;
            context.beginPath();
            context.arc(circle.x, circle.y, circle.radius, 0, Math.PI*2);
            context.fillStyle = circle.color;
            context.strokeStyle = "black";
            context.fill();
            context.stroke();
        }
        context.beginPath();
        context.moveTo(points[0].x,points[0].y);
        for (var i = 0; i < points.length; i++) {
            context.lineTo(points[i].x, points[i].y);
        }
        context.lineTo(points[0].x,points[0].y);
        context.fillStyle="rgb(128,128,128)";
        context.fill();
        context.strokeStyle="#black";
        context.stroke();
    }
};

canvas.onmouseup=function(){
    isDragging=false;
};

canvas.onmouseout=function(){
    isDragging=false;
};
