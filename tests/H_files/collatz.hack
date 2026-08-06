


var collatz(x){
    if (x%2 == 0){
        return x/2;
    } else {
        return 3*x+1;
    }
}

var main(){
    var num = 27;
    while (num>1){
        num = collatz(num);
    }
    return num
}



