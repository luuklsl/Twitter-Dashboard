(function($, block) {

// Entity formatters for use by tweet list
var entity_formatters = {
    'urls': function(e) {
        return '<a href="' + e.url + '">' + e.display_url + '</a>';
    },
    
    'user_mentions': function(e) {
        return '<a href="https://twitter.com/'+e.screen_name+'">@'+e.screen_name+'</a>';
    },

    'hashtags': function(e) {
        return '<a href="https://twitter.com/hashtag/'+e.text+'?src=hash">#' +e.text+'</a>';
    },

    'default': function(e) {
        return '{ENTITY}';
    }
};

// processes entities for the given message and entity object
var process_entities = function(message, entities) {
    // short-circuit failure mode
    if(typeof entities === 'undefined') {
        return message;
    }

    // build list of entities sorted on starting index
    var es = [];

    $.each(entities, function(t, ts) {
        $.each(ts, function(_, e) {
            e['type'] = t;
            es.push(e);
        });
    });

    es.sort(function(a,b) {
        return a['indices'][0] - b['indices'][0];
    });

    // process entities one-by-one in order of appearance
    var marker = 0;
    var result = "";
    for(var i in es) {
        var e = es[i];
        var start = e['indices'][0];
        var stop = e['indices'][1];

        //copy string content
        result += message.substring(marker, start);

        //process entity (through formatter or no-op function)
        var formatter = entity_formatters[e.type]
                        || function(e) { return message.substring(start,stop) };
        result += formatter(e);

        // update marker location
        marker = stop;
    }

    // append tail of message
    result += message.substring(marker, message.length);

    return result;
}

var avatars = [
  'adult_brick_brunette_child_clothes_clothing_fashion_598753.jpg',
  'adult_child_clothes_clothing_farm_female_fern_598204.jpg',
  'adventure_child_couple_girl_high_hiking_landscape_597929.jpg',
  'adventure_child_female_fish_girl_goggles_gun_light_598580.jpg',
  'adventure_climbing_daytime_grass_hiker_hiking_hill_598288.jpg',
  'band_boy_child_concert_dark_fashion_fun_girl_598929.jpg',
  'beachcomber_atlantic_ocean_silhouette_228374.jpg',
  'beautiful_child_dress_eyes_fashion_female_girl_hat_599122.jpg',
  'carefree_child_female_field_freedom_fun_girl_grass_598912.jpg',
  'fashion_girl_187287.jpg'
]

block.fn.tweets = function(config) {
    var options = $.extend({
        memory: 20
    }, config);

    // create the necessary HTML in the block container
    this.$element.append('<ol class="tweet-list stream-items"></ol>');

    // store list for later
    var $list = this.$element.find('ol');


    // register default handler for handling tweet data
    i = Math.round(Math.random(8)*9);
    this.actions(function(e, tweet){
      var tweets = [];
      if ( typeof tweet.buffer != 'undefined' ) {
        if ( $('.stream-item').length > 0 ) {
          return;
        }
        for ( var j = 0; j < options.memory; j++ ) {
          tweets.push(tweet.buffer.tweets[j])
        }
      }
      else {
        tweets = [tweet.tweet];
      }
      if ( tweets.length > 0 ) {
        tweets.map(function(tweet) {
          var $item = $('<li class="stream-item"></li>');
        
          var $tweet = $('<div class="tweet"></div>');
          var $content = $('<div class="content"></div>');
          var $header = $('<div class="stream-item-header"></div>');
        
          // Build a tag image and header:
          var $account = $('<a class="account-group"></a>');
          $account.attr("href", "http://twitter.com/" + tweet.user.screen_name);
        
          var $avatar = $("<img>").addClass("avatar");
          i++
          if ( i > 9 ) {
            i = 0
          }
          $avatar.attr("src", '/img/profile_pic/' + avatars[i]);
          $account.append($avatar);
          $account.append($('<strong class="fullname">' + tweet.user.name + '</strong>'));
          $account.append($('<span>&nbsp;</span>'));
          $account.append($('<span class="username"><s>@</s><b>' + tweet.user.screen_name + '</b></span>'));
          $header.append($account);
        
          var tweet_created_at = tweet.created_at.replace("+0000",'') 
          // Build timestamp:
          var $time = $('<small class="time"></small>');
          $time.append($('<span>' + tweet_created_at + '</span>'));
        
          $header.append($time);
          $content.append($header);
        
          // Build contents:
          var text = process_entities(tweet.text, tweet.entities);
          var $text = $('<p class="tweet-text">' + text + '</p>');
          $content.append($text);
        
          // Build outer structure of containing divs:
          $tweet.append($content);
          $item.append($tweet);
          
          // place new tweet in front of list 
          $list.prepend($item);
        
          // remove stale tweets
          if ($list.children().size() > options.memory) {
              $list.children().last().remove();
          }
        })
      }
    });

    return this.$element;
};
})(jQuery, block);
