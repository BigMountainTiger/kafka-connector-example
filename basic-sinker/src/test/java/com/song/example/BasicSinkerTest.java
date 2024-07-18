package com.song.example;

import org.junit.Test;

public class BasicSinkerTest {

	@Test
	public void Test() throws Exception {
		
		String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
		SQLlogger slogger = new SQLlogger(url, "postgres", "docker");
		
		slogger.log("Example test message");
	}
}
