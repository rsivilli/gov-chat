(
    function(){
        /*** Register plugin in window object */
        this.govChat = function(){
            let defaults = {
                chat_url:"localhost:8000/chat"
            };
            this.chat = [];
            this.elements = [];
            this.settings = (arguments[0] && typeof arguments[0]==='object') ? extendDefaults(defaults,arguments[0]): defaults;

            this.init();
        }

        /*** Public methods */
        govChat.prototype.init = function(){
            console.log("Init plugin.");
            build.call(this);
        }

        govChat.prototype.update = function(element){
            console.log("Update plugin.");
        }

        govChat.prototype.test = function(){
            console.log("derp");
        }
        
        govChat.prototype.chat = async function(question){
            const res = await fetch("",  {body: JSON.stringify(question)});
            return await res.json();
        }

    

        /*** Private methods */

        function build(element){
            console.log("Build plugin.");
        }

        function extendDefaults(defaults,properties){
            Object.keys(properties).forEach(property => {
                if(properties.hasOwnProperty(property)){
                    defaults[property] = properties[property];
                }
            })
            return defaults
        }


    }()
);