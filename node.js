const Discord = require('discord.js');

const ytdl = require('ytdl-core');

const client = new Discord.Client();

const prefix = '!'; // Change this to your desired command prefix

// Queue to store the music

const queue = new Map();

const statuses = [

  { name: 'R', url: 'https://twitch.tv/gtav' },

  { name: 'RI', url: 'https://twitch.tv/gtav' },

  { name: 'RIF', url: 'https://twitch.tv/gtav' },

  { name: 'RIFI', url: 'https://twitch.tv/gtav' },

  { name: 'RIFIN', url: 'https://twitch.tv/gtav' },

  { name: 'RIFINO', url: 'https://twitch.tv/gtav' }

];

let statusIndex = 0;

client.once('ready', () => {

  console.log('Bot is ready!');

  setInterval(changeStatus, 4000);

});

function changeStatus() {

  const status = statuses[statusIndex];

  client.user.setPresence({

    activity: { name: status.name, type: 'STREAMING', url: status.url }

  });

  statusIndex = (statusIndex + 1) % statuses.length;

}

client.on('message', async (message) => {

  if (!message.content.startsWith(prefix) || message.author.bot) return;

  const args = message.content.slice(prefix.length).trim().split(' ');

  const command = args.shift().toLowerCase();

  if (command === 'play') {

    execute(message, args);

  } else if (command === 'skip') {

    skip(message);

  } else if (command === 'pause') {

    pause(message);

  } else if (command === 'resume') {

    resume(message);

  }

});

async function execute(message, args) {

  const voiceChannel = message.member.voice.channel;

  if (!voiceChannel) {

    return message.channel.send('You need to be in a voice channel to play music!');

  }

  const permissions = voiceChannel.permissionsFor(message.client.user);

  if (!permissions.has('CONNECT') || !permissions.has('SPEAK')) {

    return message.channel.send('I need permissions to join and speak in your voice channel!');

  }

  const songInfo = await ytdl.getInfo(args[0]);

  const song = {

    title: songInfo.videoDetails.title,

    url: songInfo.videoDetails.video_url,

  };

  let serverQueue = queue.get(message.guild.id);

  if (!serverQueue) {

    const queueContruct = {

      textChannel: message.channel,

      voiceChannel: voiceChannel,

      connection: null,

      songs: [],

      playing: true,

    };

    queue.set(message.guild.id, queueContruct);

    queueContruct.songs.push(song);

    try {

      const connection = await voiceChannel.join();

      queueContruct.connection = connection;

      play(message.guild, queueContruct.songs[0]);

    } catch (error) {

      console.error(error);

      queue.delete(message.guild.id);

      return message.channel.send('There was an error playing the music!');

    }

  } else {

    serverQueue.songs.push(song);

    return message.channel.send(`**${song.title}** has been added to the queue!`);

  }

}

function skip(message) {

  const serverQueue = queue.get(message.guild.id);

  if (!message.member.voice.channel) {

    return message.channel.send('You need to be in a voice channel to skip the music!');

  }

  if (!serverQueue) {

    return message.channel.send('There are no songs in the queue to skip!');

  }

  serverQueue.connection.dispatcher.end();

}

function pause(message) {

  const serverQueue = queue.get(message.guild.id);

  if (!message.member.voice.channel) {

    return message.channel.send('You need to be in a voice channel to pause the music!');

  }

  if (!serverQueue) {

    return message.channel.send('There is no music currently playing!');

  }

  if (serverQueue.connection.dispatcher.paused) {

    return message.channel.send('The music is already paused!');

  }

  serverQueue.connection.dispatcher.pause();

  message.channel.send('The music has been paused!');

}

function resume(message) {

  const serverQueue = queue.get(message.guild.id);

  if (!message.member.voice.channel) {

    return message.channel.send('You need to be in a voice channel to resume the music!');

  }

  if (!serverQueue) {

    return message.channel.send('There is no music to resume!');

  }

  if (!serverQueue.connection.dispatcher.paused) {

    return message.channel.send('The music is already playing!');

  }

  serverQueue.connection.dispatcher.resume();

  message.channel.send('The music has been resumed!');

}

function play(guild, song) {

  const serverQueue = queue.get(guild.id);

  if (!song) {

    serverQueue.voiceChannel.leave();

    queue.delete(guild.id);

    return;

  }

  const dispatcher = serverQueue.connection

    .play(ytdl(song.url))

    .on('finish', () => {

      serverQueue.songs.shift();

      play(guild, serverQueue.songs[0]);

    })

    .on('error', (error) => {

      console.error(error);

    });

  dispatcher.setVolumeLogarithmic(0.5);

  serverQueue.textChannel.send(`Start playing: **${song.title}**`);

}

// Replace 'YOUR_TOKEN' with your own Discord bot token

client.login('YOUR_TOKEN');

