// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Global variable containing the query we'd like to pass to Flickr. In this
 * case, kittens!
 *
 * @type {string}
 */
 
function addtokeepcdreadlist2(fid){var d=document,z=d.createElement('scr'+'ipt'),b=d.body,l=d.location;try{if(!b)throw(0);d.title='(Saving...) '+d.title;z.setAttribute('src',l.protocol+'//www.keepcd.com/readlist/api/adding?u='+encodeURIComponent(l.href)+'&t='+(new Date().getTime())+'&f='+fid);b.appendChild(z);}catch(e){alert('请等待页面加载完毕.');}}

 
function addtokeepcdreadlist(id){
      var a = document.createElement("a");
      a.innerText = "test";
      document.getElementById("folders").appendChild(a);
}
    
var folderGenerator = {
  /**
   * Flickr URL that will give us lots and lots of whatever we're looking for.
   *
   * See http://www.flickr.com/services/api/flickr.photos.search.html for
   * details about the construction of this URL.
   *
   * @type {string}
   * @private
   */


  searchOnKeepCD_: 'http://www.keepcd.com/readlist/api/folders',

  /**
   * Sends an XHR GET request to grab photos of lots and lots of kittens. The
   * XHR's 'onload' event is hooks up to the 'showPhotos_' method.
   *
   * @public
   */


  requestFolders: function() {
    var req = new XMLHttpRequest();
    req.open("GET", this.searchOnKeepCD_, true);
    // req.onload = this.showFolders_.bind(this);
    req.onreadystatechange = function () {
    if ( req.readyState == 4 && req.status == 200 ) {
          res = JSON.parse( req.responseText );
          for (var i = 0; i < res.length; i++){
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.setAttribute('href', 'javascript:addtokeepcdreadlist("'+res[i].id+'");');
            a.innerText = res[i].title;
            li.appendChild(a);
            if(document.body != null){ document.getElementById('folders').appendChild(li); }
          }
        }
    };

    req.send(null);
  },

  /**
   * Handle the 'onload' event of our kitten XHR request, generated in
   * 'requestKittens', by generating 'img' elements, and stuffing them into
   * the document for display.
   *
   * @param {ProgressEvent} e The XHR ProgressEvent.
   * @private
   */
  showFolders_: function (e) {

    //if ( xmlHttp.readyState == 4 && xmlHttp.status == 200 ) 
     
      // var d = document.createElement('div');
      // d.innerText = e.target.responseText;
      // document.body.appendChild(d);
      var res =  e.target.responseText ;
      for (var i = 0; i < res.length; i++){
        // var a = this.constructAddingURL_(res[i]);
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.setAttribute('href', 'http://www.keepcd.com/readlist/api/adding?f='+res[i].id);
        a.innerText = res[i].title;
        li.appendChild(a);
        // document.getElementsByTagName('body')[0].appendChild(a);
        if(document.body != null){ document.getElementById('folders').appendChild(li); }
      }
     
  },

  /**
   * Given a photo, construct a URL using the method outlined at
   * http://www.flickr.com/services/api/misc.urlKittenl
   *
   * @param {DOMElement} A kitten.
   * @return {string} The kitten's URL.
   * @private
   */
  constructAddingURL_: function (folder) {
    var d=document,z=d.createElement('scr'+'ipt'),b=d.body,l=d.location;

    return "<a href='http://www.keepcd.com/readlist/api/adding?f="+folder.id+"&u="+encodeURIComponent(l.href)+"'>"+folder.title+"</a>";

  }
};

// Run our kitten generation script as soon as the document's DOM is ready.
document.addEventListener('DOMContentLoaded', function () {
  folderGenerator.requestFolders();
});
