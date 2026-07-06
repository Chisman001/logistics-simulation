class Layout {

    static locationPosition(location) {

        switch (location) {

            case "POINT_A":
                return { x: 100, y: 150 };

            case "POINT_C":
                return { x: 900, y: 150 };

            default:
                return { x: 500, y: 150 };

        }

    }

    static truckPosition(location, index) {

        const base = this.locationPosition(location);

        return {

            x: base.x + (index % 3) * 90,

            y: base.y + Math.floor(index / 3) * 70

        };

    }

    static tankPosition(location, index) {

        const base = this.locationPosition(location);

        return {

            x: base.x + (index % 3) * 70,

            y: base.y + 170 + Math.floor(index / 3) * 60

        };

    }

}