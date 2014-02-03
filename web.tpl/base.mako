<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width">

  <title>
      <%block name="title">Somebody forgot to set a title</%block>
  </title>

    <link href='http://fonts.googleapis.com/css?family=Open+Sans:600|Montserrat:700' rel='stylesheet' type='text/css'>
    <link href="/static/style.css" media="screen, projection" rel="stylesheet" type="text/css" />


  <!-- Meta -->
  <meta content="winnie" property="og:title">
  <meta content="An IRC bot with a few features." name="description">

  <script src="//ajax.googleapis.com/ajax/libs/prototype/1.7.1.0/prototype.js"></script>
  <script src="/static/winnie.js"></script>

</head>
<body>
    <div class="header">
        <nav>
        <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/streams">Streams</a></li>
            <li><a href="/intel">Intel</a></li>
            <li><a href="/archives">Archives</a></li>
        </ul>
        </nav>
    </div>


    <div class="splash">
        <h1>much wow, such oblige</h1>

        <div class="fill">

        </div>

        <%block name="callout"></%block>
    </div>

    <div class="sidebar">
    </div>

    ${self.body()}
</body>
</html>
