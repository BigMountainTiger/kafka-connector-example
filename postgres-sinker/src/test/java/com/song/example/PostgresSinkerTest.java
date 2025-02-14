package com.song.example;

import org.junit.Test;

public class PostgresSinkerTest {

	@Test
	public void Test() throws Exception {
		String url = "jdbc:postgresql://localhost:5432/postgres";
		SQLSinker sinker = new SQLSinker(url, "postgres", "docker");

		String sql_upsert = "call public.simple_schema_table_upsert(%s, %s)";
		String sql_delete = "call public.simple_schema_table_delete(%s)";

		// Insert
		sinker.put(sql_upsert, new String[] { "1", "initial value" });
		sinker.put(sql_upsert, new String[] { "2", "initial value" });
		sinker.put(sql_upsert, new String[] { "3", "initial value" });


		sinker.flush();

		// Update
		sinker.put(sql_upsert, new String[] { "1", "Updated" });
		sinker.put(sql_upsert, new String[] { "2", "Updated" });
		sinker.put(sql_upsert, new String[] { "3", "Updated" });

		// This similate a failure by inerting duplicate primary key to test the flush runs in a transaction
		// var insert = "insert into public.simple_schema_table values(%s, %s)";
		// sinker.put(insert, new String[] { "3", "Should Fail" });

		sinker.flush();

		// Delete
		sinker.put(sql_delete, new String[] { "1" });
		sinker.put(sql_delete, new String[] { "2" });

		// Test handling of null, quotes, and non-string data types
		sinker.put(sql_upsert, new Object[] { 3, null});
		sinker.put(sql_upsert, new Object[] { 4, "With '/\" quotes"});

		sinker.flush();
	}
}
