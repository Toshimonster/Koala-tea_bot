init = () => {
    var portal = document.getElementById('koala')
    var canvas = document.getElementById('canvas')
    var ctx = canvas.getContext('2d')
    var [red, green, blue, iter] = [0, 0, 0, 0]

    resize = () => {
        canvas.height = innerHeight
        canvas.width = innerWidth
    }
    resize()
    window.addEventListener('resize', function() {
        resize();
    });

    draw = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = `rgb(${Math.floor(red)}, ${Math.floor(green)}, ${Math.floor(blue)})`
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        if (Math.floor(iter / 50) % 2 == 0) {
            red -= 0.1
            blue -= 0.1
            green -= 1
        } else {
            red -= 0.1
            blue -= 0.1
            green -= 1
        }
        iter += 1

        animation()

        requestAnimationFrame(draw);
    }

    animation = () => {

        if (iter > 100 && iter < 1100) {
            ctx.translate(canvas.width / 2, canvas.height / 2)
            ctx.globalAlpha = (iter - 100) / 1000
            ctx.rotate(iter * Math.PI / 1000)
            ctx.drawImage(portal, (iter - 100)*-0.512, (iter - 100)*-0.512, (iter- 100)*1.024, (iter - 100)*1.024)
            ctx.rotate(-(iter * Math.PI / 1000))
            ctx.globalAlpha = 1
            ctx.translate(-(canvas.width / 2), -(canvas.height / 2))
        } else if (iter > 100) {
            ctx.translate(canvas.width / 2, canvas.height / 2)
            ctx.rotate(iter * Math.PI / 1000)
            ctx.drawImage(portal, - 512, - 512, 1024, 1024)
            ctx.rotate(-(iter * Math.PI / 1000))
            ctx.translate(-(canvas.width / 2), -(canvas.height / 2))
        }

        ctx.translate(canvas.width / 2, canvas.height / 2)
        ctx.font = "100px Comic Sans MS";
        ctx.fillStyle = "red";
        ctx.textAlign = "center";
        ctx.fillText("Now this is a koala-tea bot!", 0, 100);
        ctx.translate(-(canvas.width / 2), -(canvas.height / 2))

    }

    draw();
    requestAnimationFrame(draw);
}
