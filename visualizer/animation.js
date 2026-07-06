class Animator {

    static move(current, target) {

        const speed = 0.03;

        return current + (target - current) * speed;

    }

}