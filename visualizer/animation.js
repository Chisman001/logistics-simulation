class Animator {

    static move(current, target) {

        const speed = 0.12;

        return current + (target - current) * speed;

    }

}