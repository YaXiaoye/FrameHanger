<script type="text/javascript">

    //Mutation observation to capture iframe injection
    MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
    var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
    //console.log(mutation);
    for(var j=0; j<mutation.addedNodes.length; ++j) {
         var node = mutation.addedNodes[j];
         if ((node.nodeName === 'IFRAME') && (typeof node.src != 'undefined') )
         {
            console.log(node);
            console.log("[mutationObserve][iframe][summary]" + "src" + "->" + node.src);
            console.log("[mutationObserve][iframe][summary]" + "width" + "->" + node.width);
            console.log("[mutationObserve][iframe][summary]" + "height" + "->" + node.height);
            if (typeof node.style != 'undefined')
                {console.log("[mutationObserve][iframe][summary]" + "style" + "->" + node.style.cssText);}
            else
                {console.log("[mutationObserve][iframe][summary]" + "style" + "->" + node.style);}
            console.log("[mutationObserve][iframe][summary]" + "sandbox" + "->" + node.sandbox);

         }
        }
    });
});

var observerConfig = {
        childList: true,
        subtree: true
};

observer.observe(document, observerConfig);
</script>

