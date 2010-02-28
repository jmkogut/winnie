// winnie index script

(function($){ 
    $.fn.extend({ 
        periodic_populate: function(interval, getter, watcher) { 
            var panel = this;
            
            panel.populate(getter);
            $(panel).attr("interval", setInterval(function() {
                if (!watcher()) clearInterval($(panel).attr("interval"));
                panel.populate(getter);
            }, interval));

            return $(); 
        }, 
        populate: function(getter) { 
            var panel = this;

            getter(this);

            return $();
        },
        
        replace_items: function(data, handler) {
            $(this).find("ul.items").html("");
            this.add_items(data, handler);
        },

        add_items: function(data, handler) {
            //console.log("Called add_items");
            //console.log(data);

            var panel = this;

            $.each(data, function(i, item) {
                var li = $("<li/>").append(item);
                if (handler) {
                    li.clickable(function(){
                        handler(item);
                    });
                }
                li.appendTo($(panel).find("ul.items"));

            });               
            
            $(panel).find("ul.items").scroll_bottom();

            return $();
        },
        
        scroll_bottom: function()
        {
            $(this).attr("scrollTop", $(this).attr("scrollHeight"));
            return $();
        },
        
        clickable: function(handler)
        {
            $(this).click(handler);
            $(this).addClass("clickable");
        }
    }); 
})(jQuery);

Array.prototype.map = function(fn) {
    var r = [];
    var l = this.length;
    for(i=0;i<l;i++)
    {
        r.push(fn(this[i]));
    }
    return r; 
};

// Model definition
function Model()
{
    //console.log("Started model.");
}

Model.prototype.EntityAction = function(entity, action, ref, callback)
{
    var url = "/"+entity+"/"+action + ((ref == "") ? "" : "/"+ref);
    this.WebRequest(url, callback);
}

Model.prototype.WebRequest = function(url, callback)
{
    $.getJSON(url, function(data) {
        //console.log("Requested "+url);

        if (data.error) {
            alert("Check console for error.");
            //console.log(data.error);
        } else {
            //console.log(callback);
            callback(data.response);
        }
    });   
}

// Main class
function Winnie(choices, output, detail)
{
    //console.log("Started winnie.");

    this.choicesContainer = choices;
    this.watchContainer = output;
    this.detailContainer = detail;

    this.updateInterval = 1500;
}

Winnie.prototype.view_channel = function(channel)
{
    var winnie = this;
    var panel = this.watchContainer;

    $(panel).attr("channel", channel);
    $(panel).attr("ref", "");

    $(panel).find("ul.items").html("");

    $(panel).periodic_populate(this.updateInterval,
        function(panel) { // Getter
            new Model().EntityAction(
                "log",
                $(panel).attr("channel").replace("#","_"),
                $(panel).attr("ref"),
                function(data) {
                    data.reverse();
                    events = [];
                    $.each(data, function(i, e) {
                        if (e.ref != $(panel).attr("ref")) {
                            events.push(winnie.format_event(e));
                            $(panel).attr("ref", e.ref);
                        }
                    });

                    panel.add_items(events);
                }
            );
        },
        function(panel) { // Watcher
                //console.log($(panel).find("ul.items"));
            
            return ($(panel).attr("channel") != "")
        }
    );
}

Winnie.prototype.pick_channel = function()
{   
    var winnie = this;

    $(this.detailContainer).hide();

    this.get_choices("",
    function(adder) // Getter
    {
        new Model().EntityAction(
            "channel",
            "list",
            "",
            adder
        );

    },
    function(channel) // Handler
    {
        winnie.view_channel(channel);
    });
}

Winnie.prototype.get_choices = function(help, getter, handler)
{
    var winnie = this;

    var format = function(item)
    {
        var span = $("<span/>").text(item);
        return span;
    };

    var panel = this.choicesContainer;

    $(panel).populate(function(panel){
        getter( function(data){panel.replace_items(data, handler);});   
    });

    $(panel).find("h2").text(help);
}

Winnie.prototype.view_mask = function(account_mask)
{
    console.log("Event incoming.");

    $(this.watchContainer).hide();
    $(this.detailContainer).show();

    this.set_detail("account mask", account_mask);
}

Winnie.prototype.set_detail = function(name, summary) {
    var panel = $(this.detailContainer);

    $(panel).find(".title").text(name);
    $(panel).find(".summary").text(summary);
}

Winnie.prototype.format_event = function(e)
{
    var winnie = this;

    var argument = $("<span/>").attr("class", "event");

    var source = $("<span/>").attr("class","source").text(e.source.split("!")[0]);
    argument.append(source);

    var arg = $("<span/>").attr("class","argument").text(e.arguments[0]);
    argument.append(arg);

    
    $(source).clickable(function() {
        winnie.view_mask(e.source);
    });

    return argument;   
}

Winnie.prototype.get_item_container = function() {
    return $("<div/>").content($("<ul/>").addClass("items"))
}
