class Bot {
    static owner_ids() {
        return [701009836938231849,703135131459911740,708233854640455740]
    }

    static dba() {
        return process.env.mongo_server
    }

    static bled() {
        return false
    }

    static owners() {
        return [701009836938231849,703135131459911740,708233854640455740]
    }

    static managers(){
        
    }

    static infinityEmoji(){
        return '<a:infinity:874548940610097163>'
    }
}

module.exports = Bot